import { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { submissionApi } from '../services/api';

function StatusBadge({ status }) {
    const colors = {
        pending: 'bg-yellow-100 text-yellow-800',
        in_progress: 'bg-blue-100 text-blue-800',
        completed: 'bg-green-100 text-green-800',
        failed: 'bg-red-100 text-red-800'
    };

    return (
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[status]}`}>
            {status.replace('_', ' ').toUpperCase()}
        </span>
    );
}

export default function Submissions() {
    const [submissions, setSubmissions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [sortConfig, setSortConfig] = useState({ key: 'created_at', direction: 'desc' });
    const [filters, setFilters] = useState({
        status: '',
        startup: '',
        platform: ''
    });

    useEffect(() => {
        fetchSubmissions();
    }, []);

    const fetchSubmissions = async () => {
        try {
            const data = await submissionApi.getAll();
            setSubmissions(data);
        } catch (error) {
            console.error('Error fetching submissions:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSort = (key) => {
        setSortConfig((prev) => ({
            key,
            direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
        }));
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const filteredAndSortedSubmissions = useMemo(() => {
        let result = [...submissions];

        // Apply filters
        if (filters.status) {
            result = result.filter(s => s.status === filters.status);
        }
        if (filters.startup) {
            result = result.filter(s => 
                s.startup?.name.toLowerCase().includes(filters.startup.toLowerCase())
            );
        }
        if (filters.platform) {
            result = result.filter(s => 
                s.platform?.name.toLowerCase().includes(filters.platform.toLowerCase())
            );
        }

        // Apply sorting
        result.sort((a, b) => {
            let aValue, bValue;
            switch (sortConfig.key) {
                case 'startup':
                    aValue = a.startup?.name || '';
                    bValue = b.startup?.name || '';
                    break;
                case 'platform':
                    aValue = a.platform?.name || '';
                    bValue = b.platform?.name || '';
                    break;
                case 'status':
                    aValue = a.status;
                    bValue = b.status;
                    break;
                case 'created_at':
                default:
                    aValue = new Date(a.created_at);
                    bValue = new Date(b.created_at);
            }

            if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
            if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
            return 0;
        });

        return result;
    }, [submissions, sortConfig, filters]);

    const SortIcon = ({ column }) => {
        if (sortConfig.key !== column) return null;
        return (
            <span className="ml-2">
                {sortConfig.direction === 'asc' ? '↑' : '↓'}
            </span>
        );
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    return (
        <div>
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-xl font-semibold text-gray-900">Submissions</h1>
                    <p className="mt-2 text-sm text-gray-700">
                        A list of all startup submissions and their current status.
                    </p>
                </div>
            </div>

            {/* Filters */}
            <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div>
                    <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                        Status
                    </label>
                    <select
                        id="status"
                        name="status"
                        value={filters.status}
                        onChange={handleFilterChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                        <option value="">All Statuses</option>
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                        <option value="failed">Failed</option>
                    </select>
                </div>
                <div>
                    <label htmlFor="startup" className="block text-sm font-medium text-gray-700">
                        Startup Name
                    </label>
                    <input
                        type="text"
                        id="startup"
                        name="startup"
                        value={filters.startup}
                        onChange={handleFilterChange}
                        placeholder="Filter by startup..."
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>
                <div>
                    <label htmlFor="platform" className="block text-sm font-medium text-gray-700">
                        Platform Name
                    </label>
                    <input
                        type="text"
                        id="platform"
                        name="platform"
                        value={filters.platform}
                        onChange={handleFilterChange}
                        placeholder="Filter by platform..."
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                </div>
            </div>

            <div className="mt-8 flex flex-col">
                <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                        <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                            <table className="min-w-full divide-y divide-gray-300">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th 
                                            scope="col" 
                                            className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6 cursor-pointer"
                                            onClick={() => handleSort('startup')}
                                        >
                                            Startup
                                            <SortIcon column="startup" />
                                        </th>
                                        <th 
                                            scope="col" 
                                            className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 cursor-pointer"
                                            onClick={() => handleSort('platform')}
                                        >
                                            Platform
                                            <SortIcon column="platform" />
                                        </th>
                                        <th 
                                            scope="col" 
                                            className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 cursor-pointer"
                                            onClick={() => handleSort('status')}
                                        >
                                            Status
                                            <SortIcon column="status" />
                                        </th>
                                        <th 
                                            scope="col" 
                                            className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 cursor-pointer"
                                            onClick={() => handleSort('created_at')}
                                        >
                                            Created At
                                            <SortIcon column="created_at" />
                                        </th>
                                        <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                            <span className="sr-only">Actions</span>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200 bg-white">
                                    {filteredAndSortedSubmissions.map((submission) => (
                                        <tr key={submission.id}>
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                                                <div className="font-medium text-gray-900">
                                                    {submission.startup?.name || 'Unknown Startup'}
                                                </div>
                                                {submission.startup?.tagline && (
                                                    <div className="text-gray-500">{submission.startup.tagline}</div>
                                                )}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                <div className="font-medium text-gray-900">
                                                    {submission.platform?.name || 'Unknown Platform'}
                                                </div>
                                                <div className="text-gray-500">
                                                    {submission.platform?.submission_type?.toUpperCase()}
                                                </div>
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                <StatusBadge status={submission.status} />
                                                {submission.error_message && (
                                                    <div className="mt-1 text-xs text-red-600">
                                                        {submission.error_message}
                                                    </div>
                                                )}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                {new Date(submission.created_at).toLocaleString()}
                                            </td>
                                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                {submission.startup && (
                                                    <Link
                                                        to={`/startups/${submission.startup_id}`}
                                                        className="text-indigo-600 hover:text-indigo-900"
                                                    >
                                                        View Startup<span className="sr-only">, {submission.startup.name}</span>
                                                    </Link>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                    {filteredAndSortedSubmissions.length === 0 && (
                                        <tr>
                                            <td colSpan="5" className="px-6 py-4 text-center text-sm text-gray-500">
                                                No submissions found
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
} 