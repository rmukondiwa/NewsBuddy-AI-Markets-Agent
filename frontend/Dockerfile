FROM nginx:1.27-alpine

COPY public /public
RUN cp /public/* /usr/share/nginx/html

EXPOSE 80

# awkwardly replace Environment variables in frontend code
COPY ./bin/inject-env.sh /
RUN chmod a+x /inject-env.sh
# need to run it this way to have access to Environment variables defined in .env
ENTRYPOINT ["/inject-env.sh", "/public/app.js"]
CMD ["nginx", "-g", "daemon off;"]
