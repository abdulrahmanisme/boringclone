import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { startupApi } from '../services/api';

export default function StartupForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        website: '',
        description: '',
        tagline: '',
        founded_year: new Date().getFullYear(),
        twitter_handle: '',
        linkedin_url: '',
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            await startupApi.createStartup(formData);
            toast.success('Startup added successfully!');
            navigate('/');
        } catch (error) {
            console.error('Error creating startup:', error);
            toast.error('Failed to add startup. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto py-8 px-4">
            <h1 className="text-2xl font-bold mb-6">Add New Startup</h1>
            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                        Company Name
                    </label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        required
                        value={formData.name}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>

                <div>
                    <label htmlFor="website" className="block text-sm font-medium text-gray-700">
                        Website
                    </label>
                    <input
                        type="url"
                        id="website"
                        name="website"
                        required
                        value={formData.website}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>

                <div>
                    <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                        Description
                    </label>
                    <textarea
                        id="description"
                        name="description"
                        rows={4}
                        value={formData.description}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>

                <div>
                    <label htmlFor="tagline" className="block text-sm font-medium text-gray-700">
                        Tagline
                    </label>
                    <input
                        type="text"
                        name="tagline"
                        id="tagline"
                        value={formData.tagline}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>

                <div>
                    <label htmlFor="founded_year" className="block text-sm font-medium text-gray-700">
                        Founded Year
                    </label>
                    <input
                        type="number"
                        name="founded_year"
                        id="founded_year"
                        min="1900"
                        max={new Date().getFullYear()}
                        value={formData.founded_year}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>

                <div>
                    <label htmlFor="twitter_handle" className="block text-sm font-medium text-gray-700">
                        Twitter Handle
                    </label>
                    <div className="mt-1 flex rounded-md shadow-sm">
                        <span className="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 bg-gray-50 px-3 text-gray-500 sm:text-sm">
                            @
                        </span>
                        <input
                            type="text"
                            name="twitter_handle"
                            id="twitter_handle"
                            value={formData.twitter_handle}
                            onChange={handleChange}
                            className="block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        />
                    </div>
                </div>

                <div>
                    <label htmlFor="linkedin_url" className="block text-sm font-medium text-gray-700">
                        LinkedIn URL
                    </label>
                    <input
                        type="url"
                        name="linkedin_url"
                        id="linkedin_url"
                        value={formData.linkedin_url}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        placeholder="https://linkedin.com/company/..."
                    />
                </div>

                <div>
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                            loading ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                    >
                        {loading ? 'Adding...' : 'Add Startup'}
                    </button>
                </div>
            </form>
        </div>
    );
} 