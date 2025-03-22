import axios from "axios";

const apiClient = axios.create({
    baseURL:import.meta.env.VITE_APP_BASE_URL,
});

apiClient.defaults.withCredentials = true;

export default apiClient;
