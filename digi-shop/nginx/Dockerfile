FROM nginx:latest

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Create necessary directories
RUN mkdir -p /src/staticfiles /src/media /src/logs

EXPOSE 80 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]