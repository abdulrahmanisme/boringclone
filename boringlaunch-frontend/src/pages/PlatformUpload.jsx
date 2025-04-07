import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { platformApi } from '../services/api';

export default function PlatformUpload() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
            setFile(selectedFile);
        } else {
            toast.error('Please select a valid Excel file (.xlsx)');
            e.target.value = null;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            toast.error('Please select a file to upload');
            return;
        }

        setLoading(true);

        try {
            await platformApi.uploadExcel(file);
            toast.success('Platforms uploaded successfully!');
            navigate('/');
        } catch (error) {
            console.error('Error uploading platforms:', error);
            toast.error('Failed to upload platforms. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto py-8 px-4">
            <h1 className="text-2xl font-bold mb-6">Upload Platforms</h1>
            <div className="bg-white shadow sm:rounded-lg p-6">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                            Excel File (.xlsx)
                        </label>
                        <div className="mt-1">
                            <input
                                type="file"
                                id="file"
                                accept=".xlsx"
                                onChange={handleFileChange}
                                className="block w-full text-sm text-gray-500
                                  file:mr-4 file:py-2 file:px-4
                                  file:rounded-md file:border-0
                                  file:text-sm file:font-medium
                                  file:bg-indigo-50 file:text-indigo-700
                                  hover:file:bg-indigo-100"
                            />
                        </div>
                        <p className="mt-2 text-sm text-gray-500">
                            Upload an Excel file containing platform data. The file should be in .xlsx format.
                        </p>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={loading || !file}
                            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                                (loading || !file) ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                        >
                            {loading ? 'Uploading...' : 'Upload Platforms'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
} 