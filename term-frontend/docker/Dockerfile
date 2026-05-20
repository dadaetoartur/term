FROM node:22-alpine

WORKDIR /term-frontend
COPY .output ./.output

ENTRYPOINT ["node", ".output/server/index.mjs"]
