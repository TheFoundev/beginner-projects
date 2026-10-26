FROM nginx:alpine

LABEL org.opencontainers.image.title="nginx-multi-page-site" \
      org.opencontainers.image.description="Multi-page static website served by Nginx" \
      org.opencontainers.image.version="1.0.0"

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy our website files
COPY index.html about.html projects.html contact.html /usr/share/nginx/html/
COPY style.css style.css
COPY script.js /usr/share/nginx/html/script.js
COPY assets/ /usr/share/nginx/html/assets/

# Custom Nginx configuration
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
