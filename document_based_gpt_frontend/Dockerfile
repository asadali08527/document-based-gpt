# Use the official Node.js image from the Docker Hub
FROM node:16-slim

# Set the working directory in the container
WORKDIR /frontend

# Copy package.json and install dependencies
COPY package.json /frontend/
RUN npm install

# Copy the rest of the application code
COPY . /frontend/

# Build the application
RUN npm run build

# Expose the application port
EXPOSE 3000

# Serve the application
CMD ["npx", "serve", "-s", "build"]
