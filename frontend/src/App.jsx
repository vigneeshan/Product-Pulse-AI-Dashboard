import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Box, TrendingUp, AlertCircle, PlusCircle } from 'lucide-react';

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Form State
  const [formData, setFormData] = useState({
    name: '', category: 'Electronics', price: '', review_text: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchDashboardData = () => {
    axios.get('http://127.0.0.1:8000/api/dashboard/summary')
      .then(response => {
        setDashboardData(response.data);
        setLoading(false);
      })
      .catch(error => console.error("Error fetching data:", error));
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      // Send data to Python backend for AI analysis
      await axios.post('http://127.0.0.1:8000/api/products', formData);
      setFormData({ name: '', category: 'Electronics', price: '', review_text: '' });
      fetchDashboardData(); // Refresh chart with new data!
    } catch (error) {
      console.error("Error submitting product", error);
      alert("Failed to submit product.");
    }
    setIsSubmitting(false);
  };

  if (loading) return <div className="flex justify-center items-center h-screen text-xl font-semibold">Loading AI Insights...</div>;

  return (
    <div className="min-h-screen p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
          <Activity className="text-blue-600" />
          ProductPulse AI Dashboard
        </h1>
        <p className="text-gray-500 mt-2">Live Market Intelligence & NLP Sentiment Analysis</p>
      </header>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 flex items-center gap-4">
          <div className="p-4 bg-blue-100 rounded-lg text-blue-600"><Box size={24} /></div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Total Products Tracked</p>
            <h2 className="text-2xl font-bold text-gray-800">{dashboardData.total_products}</h2>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 flex items-center gap-4">
          <div className="p-4 bg-green-100 rounded-lg text-green-600"><TrendingUp size={24} /></div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Avg AI Sentiment Score</p>
            <h2 className="text-2xl font-bold text-gray-800">{dashboardData.average_product_sentiment} / 1.0</h2>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 flex items-center gap-4">
          <div className="p-4 bg-orange-100 rounded-lg text-orange-600"><AlertCircle size={24} /></div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Low Sentiment Alerts</p>
            <h2 className="text-2xl font-bold text-gray-800">{dashboardData.active_alerts}</h2>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Interactive Chart */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 lg:col-span-2">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Sentiment vs Competitor Pricing Trend</h3>
          <div className="h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dashboardData.chart_data}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis yAxisId="left" domain={[0, 1]} />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="sentiment" stroke="#10b981" name="Customer Sentiment" strokeWidth={3} />
                <Line yAxisId="right" type="monotone" dataKey="competitor_price" stroke="#3b82f6" name="Avg Competitor Price ($)" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Data Entry Form */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <PlusCircle className="text-blue-600" size={20} />
            Add Product & Review
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
              <input required type="text" name="name" value={formData.name} onChange={handleInputChange} className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. Pro Gaming Mouse" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select name="category" value={formData.category} onChange={handleInputChange} className="w-full border border-gray-300 rounded-lg p-2 outline-none">
                <option>Electronics</option>
                <option>Furniture</option>
                <option>Software</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
              <input required type="number" step="0.01" name="price" value={formData.price} onChange={handleInputChange} className="w-full border border-gray-300 rounded-lg p-2 outline-none" placeholder="99.99" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Customer Review (For AI Analysis)</label>
              <textarea required name="review_text" value={formData.review_text} onChange={handleInputChange} rows="3" className="w-full border border-gray-300 rounded-lg p-2 outline-none resize-none" placeholder="Type a review to see the AI calculate sentiment..."></textarea>
            </div>
            <button type="submit" disabled={isSubmitting} className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition duration-200">
              {isSubmitting ? 'Analyzing via AI...' : 'Submit & Analyze'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;