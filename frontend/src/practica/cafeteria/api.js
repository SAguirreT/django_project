import axios from 'axios';

const apiCafeteria = axios.create({
  baseURL: 'http://127.0.0.1:8001/api/',
});

export default apiCafeteria;
