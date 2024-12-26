FROM nginx:1.27.1-bookworm

COPY --chmod=755 tools/script.sh /bin/

COPY --chmod=644 tools/nginx.conf /etc/nginx/conf.d/default.conf

ENTRYPOINT [ "bash", "/bin/script.sh" ]