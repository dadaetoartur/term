FROM nginxinc/nginx-unprivileged:1.27-alpine

WORKDIR /usr/share/nginx/html

COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY ./src /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
