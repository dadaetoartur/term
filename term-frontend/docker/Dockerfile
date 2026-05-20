FROM node:20-alpine

WORKDIR /term-frontend
COPY . .

RUN npm i
RUN npm run build

ENTRYPOINT ["node", ".output/server/index.mjs"]
