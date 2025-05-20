import axios from 'axios';

const getDashboardData = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/v1/dashboard');
        return response.data;
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        throw error;
    }
};

export default {
    getDashboardData
}; 