import { Card } from '../ui/card';
import { 
  TrendingUp, 
  Users, 
  FileText, 
  Activity,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';

const stats = [
  { 
    label: 'Total Users', 
    value: '12,543', 
    change: '+12.5%', 
    trend: 'up',
    icon: Users,
    color: 'text-blue-600 bg-blue-50'
  },
  { 
    label: 'Documents', 
    value: '3,842', 
    change: '+8.2%', 
    trend: 'up',
    icon: FileText,
    color: 'text-green-600 bg-green-50'
  },
  { 
    label: 'Active Sessions', 
    value: '1,234', 
    change: '-3.1%', 
    trend: 'down',
    icon: Activity,
    color: 'text-orange-600 bg-orange-50'
  },
  { 
    label: 'Growth Rate', 
    value: '23.5%', 
    change: '+4.8%', 
    trend: 'up',
    icon: TrendingUp,
    color: 'text-purple-600 bg-purple-50'
  },
];

const recentActivity = [
  { id: 1, action: 'New user registered', user: 'Alice Johnson', time: '2 minutes ago' },
  { id: 2, action: 'Document uploaded', user: 'Bob Smith', time: '15 minutes ago' },
  { id: 3, action: 'Project created', user: 'Carol White', time: '1 hour ago' },
  { id: 4, action: 'Settings updated', user: 'David Brown', time: '2 hours ago' },
  { id: 5, action: 'Report generated', user: 'Eve Davis', time: '3 hours ago' },
];

export function DashboardView() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Welcome back! Here's what's happening today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label} className="p-6">
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">{stat.label}</p>
                  <p className="text-2xl text-gray-900">{stat.value}</p>
                  <div className="flex items-center gap-1">
                    {stat.trend === 'up' ? (
                      <ArrowUpRight className="w-4 h-4 text-green-600" />
                    ) : (
                      <ArrowDownRight className="w-4 h-4 text-red-600" />
                    )}
                    <span className={`text-sm ${
                      stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {stat.change}
                    </span>
                  </div>
                </div>
                <div className={`p-3 rounded-lg ${stat.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card className="p-6">
          <h2 className="text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-start gap-3 pb-4 border-b border-gray-100 last:border-0 last:pb-0">
                <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">{activity.action}</p>
                  <p className="text-sm text-gray-600">{activity.user}</p>
                </div>
                <span className="text-xs text-gray-500 flex-shrink-0">{activity.time}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Quick Actions */}
        <Card className="p-6">
          <h2 className="text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              'Create Document',
              'New Project',
              'Add User',
              'Generate Report',
              'Upload File',
              'Schedule Task'
            ].map((action) => (
              <button
                key={action}
                className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-sm text-gray-700"
              >
                {action}
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
