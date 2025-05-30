def ssl_cert_info(hostname: str) -> dict:
    """Get SSL certificate info for a website (expiry, SANs, issuer)"""
    import socket
    import ssl

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
        # Parse certificate info
        from datetime import datetime, timezone

        not_after = cert.get("notAfter") if cert else None
        not_before = cert.get("notBefore") if cert else None
        # Parse dates
        date_format = "%b %d %H:%M:%S %Y %Z"
        expiry_dt = (
            datetime.strptime(not_after, date_format).replace(tzinfo=timezone.utc)
            if isinstance(not_after, str)
            else None
        )
        issue_dt = (
            datetime.strptime(not_before, date_format).replace(tzinfo=timezone.utc)
            if isinstance(not_before, str)
            else None
        )
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        days_remaining = (expiry_dt - now).days if expiry_dt else None
        # issuer is a list of tuples of tuples, e.g. ((('countryName', 'US'),), (('organizationName', 'DigiCert Inc'),), ...)
        issuer = ""
        if cert and "issuer" in cert and cert["issuer"]:
            issuer = ", ".join(
                f"{'='.join(attr)}" if isinstance(attr, tuple) else str(attr)
                for rdn in cert["issuer"]
                for attr in rdn
            )
        sans = []
        if cert and "subjectAltName" in cert and cert["subjectAltName"]:
            sans = [x[1] for x in cert["subjectAltName"] if x[0] == "DNS"]
        output = (
            f"\nSSL Certificate info for {hostname}:\n"
            f"  Issuer: {issuer}\n"
            f"  Issue Date: {not_before}\n"
            f"  Expiry Date: {not_after}\n"
            f"  Days Remaining: {days_remaining}\n"
            f"  SANs: {', '.join(str(s) for s in sans)}\n"
        )
        return {"info": output}
    except Exception as e:
        return {"error": str(e)}
