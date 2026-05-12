FROM node:18-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all project files
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host"]
