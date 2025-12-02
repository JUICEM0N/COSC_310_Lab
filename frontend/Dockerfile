FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ENV NEXT_PUBLIC_URL=http://backend:8000

EXPOSE 3000

CMD ["npm", "run", "dev"]