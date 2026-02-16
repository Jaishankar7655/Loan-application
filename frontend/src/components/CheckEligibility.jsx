import React, { useState } from 'react';
import axios from 'axios';
import { CheckCircle, AlertCircle, Loader, DollarSign } from 'lucide-react';

const CheckEligibility = () => {
    const [formData, setFormData] = useState({
        customer_id: '',
        loan_amount: '',
        interest_rate: '',
        tenure: ''
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loanCreated, setLoanCreated] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleCheck = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);
        setLoanCreated(null);
        try {
            const res = await axios.post('http://127.0.0.1:8000/check-eligibility', formData);
            setResult(res.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Check failed. Customer might not exist.');
        } finally {
            setLoading(false);
        }
    };

    const handleCreateLoan = async () => {
        setLoading(true);
        try {
            const res = await axios.post('http://127.0.0.1:8000/create-loan', formData);
            setLoanCreated(res.data);
        } catch (err) {
            setError('Failed to create loan');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto mt-10">
            <div className="bg-white shadow-lg rounded-xl overflow-hidden p-6 mb-8">
                <div className="flex items-center space-x-3 mb-6">
                    <div className="bg-purple-100 p-3 rounded-full">
                        <CheckCircle className="h-6 w-6 text-purple-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800">Check Loan Eligibility</h2>
                </div>

                <form onSubmit={handleCheck} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Customer ID</label>
                            <input type="number" name="customer_id" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-purple-500 focus:border-purple-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Loan Amount</label>
                            <input type="number" name="loan_amount" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-purple-500 focus:border-purple-500" />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Interest Rate (%)</label>
                            <input type="number" step="0.1" name="interest_rate" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-purple-500 focus:border-purple-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Tenure (Months)</label>
                            <input type="number" name="tenure" required onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-purple-500 focus:border-purple-500" />
                        </div>
                    </div>

                    <button type="submit" disabled={loading} className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:bg-purple-400">
                        {loading ? <Loader className="animate-spin h-5 w-5" /> : 'Check Eligibility'}
                    </button>
                </form>
            </div>

            {error && (
                <div className="p-4 bg-red-50 rounded-md border border-red-200 mb-6 flex items-center">
                    <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
                    <p className="text-sm text-red-700">{error}</p>
                </div>
            )}

            {result && (
                <div className={`shadow-lg rounded-xl overflow-hidden p-6 ${result.approval ? 'bg-green-50 border border-green-200' : 'bg-orange-50 border border-orange-200'}`}>
                    <h3 className={`text-xl font-bold mb-4 ${result.approval ? 'text-green-800' : 'text-orange-800'}`}>
                        {result.approval ? 'Congratulations! Loan Approvable' : 'Loan Not Approvable'}
                    </h3>

                    <div className="grid grid-cols-2 gap-4 mb-6">
                        <div className="bg-white p-3 rounded-md shadow-sm">
                            <span className="block text-xs text-gray-500 uppercase tracking-wide">Interest Rate</span>
                            <span className="text-lg font-semibold">{result.interest_rate}%</span>
                        </div>
                        <div className="bg-white p-3 rounded-md shadow-sm">
                            <span className="block text-xs text-gray-500 uppercase tracking-wide">Corrected Rate</span>
                            <span className={`text-lg font-bold ${result.corrected_interest_rate > result.interest_rate ? 'text-orange-600' : 'text-gray-800'}`}>
                                {result.corrected_interest_rate}%
                            </span>
                        </div>
                        <div className="bg-white p-3 rounded-md shadow-sm col-span-2">
                            <span className="block text-xs text-gray-500 uppercase tracking-wide">Monthly Installment</span>
                            <span className="text-2xl font-bold text-gray-800">₹{Math.round(result.monthly_installment).toLocaleString()}</span>
                        </div>
                    </div>

                    {result.approval && !loanCreated && (
                        <button onClick={handleCreateLoan} disabled={loading} className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                            <DollarSign className="h-5 w-5 mr-2" />
                            Process & Create Loan
                        </button>
                    )}

                    {loanCreated && (
                        <div className="mt-4 p-4 bg-white rounded-md border border-green-300">
                            <h4 className="font-bold text-green-700">Loan Created Successfully!</h4>
                            <p>Loan ID: <span className="font-bold text-gray-900">{loanCreated.loan_id}</span></p>
                            <p className="text-sm text-gray-500">{loanCreated.message}</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default CheckEligibility;
