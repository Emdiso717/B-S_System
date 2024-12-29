# 使用官方的 Node.js 镜像
FROM node:20

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY / ./
RUN npm run build

# 阶段 2: 运行
FROM nginx
RUN mkdir /app
COPY --from=0 /app/dist /app
EXPOSE 80
COPY nginx.conf /etc/nginx/nginx.conf


