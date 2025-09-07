import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  FileText, 
  Plus, 
  Search, 
  Bookmark, 
  Settings, 
  HelpCircle,
  User
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { user } = useAuth();

  const menuItems = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'New Document', href: '/documents/new', icon: Plus },
    { name: 'History', href: '/dashboard', icon: FileText },
    { name: 'Search', href: '/search', icon: Search },
    { name: 'Saved', href: '/dashboard', icon: Bookmark },
    { name: 'Settings', href: '/settings', icon: Settings },
    { name: 'Support', href: '/support', icon: HelpCircle },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 shadow-lg w-64 min-h-screen">
      <div className="p-6">
        {/* Logo */}
        <div className="flex items-center space-x-2 mb-8">
          <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">IB</span>
          </div>
          <span className="text-xl font-bold text-gray-900 dark:text-white">
            InstaBrief
          </span>
        </div>

        {/* User Profile */}
        <div className="flex items-center space-x-3 mb-8 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
              {user?.full_name || 'User'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
              {user?.email || 'user@example.com'}
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.href;
            
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;