FROM python:3.13-rc-bookworm

WORKDIR /files/

COPY --chmod=755 tools/script.sh /bin/

COPY --chmod=644 tools/req.txt /tmp/

ENTRYPOINT [ "/bin/bash", "/bin/script.sh" ]