import React, { useState } from 'react';
import axios from 'axios';
import { UserPlus, Loader } from 'lucide-react';

const Register = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        age: '',
        monthly_income: '',
        phone_number: ''
    });
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResponse(null);
        try {
            const res = await axios.post('http://127.0.0.1:8000/register', formData);
            setResponse(res.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 bg-white shadow-lg rounded-xl overflow-hidden p-6">
            <div className="flex items-center space-x-3 mb-6">
                <div className="bg-indigo-100 p-3 rounded-full">
                    <UserPlus className="h-6 w-6 text-indigo-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Register Customer</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">First Name</label>
                        <input type="text" name="first_name" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Last Name</label>
                        <input type="text" name="last_name" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500" />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Age</label>
                    <input type="number" name="age" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500" />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Monthly Income</label>
                    <input type="number" name="monthly_income" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500" />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                    <input type="tel" name="phone_number" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500" />
                </div>

                <button type="submit" disabled={loading} className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400">
                    {loading ? <Loader className="animate-spin h-5 w-5" /> : 'Register'}
                </button>
            </form>

            {response && (
                <div className="mt-6 p-4 bg-green-50 rounded-md border border-green-200">
                    <h3 className="text-green-800 font-semibold">Registration Successful!</h3>
                    <p className="text-sm text-green-700">Customer ID: <span className="font-bold">{response.customer_id}</span></p>
                    <p className="text-sm text-green-700">Approved Limit: <span className="font-bold">₹{response.approved_limit}</span></p>
                </div>
            )}

            {error && (
                <div className="mt-6 p-4 bg-red-50 rounded-md border border-red-200">
                    <h3 className="text-red-800 font-semibold">Error</h3>
                    <p className="text-sm text-red-700">{JSON.stringify(error)}</p>
                </div>
            )}
        </div>
    );
};

export default Register;
