import React, { useState } from 'react';
import axios from 'axios';
import { LayoutDashboard, Search, FileText, Calendar, DollarSign, PieChart } from 'lucide-react';

const Dashboard = () => {
    const [customerId, setCustomerId] = useState('');
    const [loans, setLoans] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searched, setSearched] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!customerId) return;
        setLoading(true);
        setError(null);
        setSearched(true);
        try {
            const res = await axios.get(`http://127.0.0.1:8000/view-loans/${customerId}`);
            setLoans(res.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to fetch loans. Customer might not exist.');
            setLoans([]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto mt-10">
            <div className="bg-white shadow-sm rounded-xl p-6 mb-8 border border-gray-200">
                <div className="flex items-center space-x-3 mb-6">
                    <div className="bg-blue-100 p-3 rounded-full">
                        <LayoutDashboard className="h-6 w-6 text-blue-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800">Customer Dashboard</h2>
                </div>

                <form onSubmit={handleSearch} className="flex gap-4">
                    <div className="flex-grow">
                        <label className="sr-only">Customer ID</label>
                        <div className="relative rounded-md shadow-sm">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <Search className="h-5 w-5 text-gray-400" />
                            </div>
                            <input type="number" value={customerId} onChange={(e) => setCustomerId(e.target.value)} className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-3" placeholder="Enter Customer ID to view loans" />
                        </div>
                    </div>
                    <button type="submit" disabled={loading} className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400">
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </form>
            </div>

            {error && (
                <div className="p-4 bg-red-50 rounded-md border border-red-200 text-red-700 mb-6">
                    {error}
                </div>
            )}

            {searched && loans.length === 0 && !loading && !error && (
                <div className="text-center py-10 bg-gray-50 rounded-lg border border-dashed border-gray-300">
                    <p className="text-gray-500">No loans found for this customer.</p>
                </div>
            )}

            {loans.length > 0 && (
                <div className="grid gap-6 md:grid-cols-2">
                    {loans.map((loan) => (
                        <div key={loan.loan_id} className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow duration-300">
                            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                                <div className="flex items-center">
                                    <FileText className="h-5 w-5 text-gray-500 mr-2" />
                                    <span className="font-semibold text-gray-700">Loan #{loan.loan_id}</span>
                                </div>
                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                    Active
                                </span>
                            </div>
                            <div className="p-6">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-sm font-medium text-gray-500">Amount</p>
                                        <p className="mt-1 text-lg font-semibold text-gray-900 flex items-center">
                                            <DollarSign className="h-4 w-4 text-gray-400 mr-1" />
                                            {loan.loan_amount.toLocaleString()}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-gray-500">Interest Rate</p>
                                        <p className="mt-1 text-lg font-semibold text-gray-900 flex items-center">
                                            <PieChart className="h-4 w-4 text-gray-400 mr-1" />
                                            {loan.interest_rate}%
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-gray-500">Monthly EMI</p>
                                        <p className="mt-1 text-lg font-semibold text-gray-900">
                                            ₹{Math.round(loan.monthly_installment).toLocaleString()}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-gray-500">EMIs Left</p>
                                        <p className="mt-1 text-lg font-semibold text-gray-900 flex items-center">
                                            <Calendar className="h-4 w-4 text-gray-400 mr-1" />
                                            {loan.repayments_left}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Dashboard;
