FROM node:20-alpine

WORKDIR /term-frontend

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

ENTRYPOINT ["node", ".output/server/index.mjs"]
