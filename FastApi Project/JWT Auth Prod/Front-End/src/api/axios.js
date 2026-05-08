import axios from 'axios';

// Create a standard axios instance pointing to the FastAPI backend
const instance = axios.create({
    baseURL: 'http://localhost:8000/api', // FastAPI standard port
});

export default instance;
