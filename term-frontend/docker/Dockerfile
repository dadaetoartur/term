FROM node:22-alpine

WORKDIR /term-frontend

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

ENTRYPOINT ["node", ".output/server/index.mjs"]
