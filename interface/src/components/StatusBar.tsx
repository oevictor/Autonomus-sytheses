import { Wifi, HardDrive, Activity } from 'lucide-react';

export function StatusBar() {
  return (
    <footer className="h-8 bg-gray-900 text-gray-300 flex items-center justify-between px-4 text-xs flex-shrink-0">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5">
          <Wifi className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Connected</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5" />
          <span className="hidden md:inline">CPU: 23%</span>
        </div>
        <div className="flex items-center gap-1.5">
          <HardDrive className="w-3.5 h-3.5" />
          <span className="hidden md:inline">Storage: 45.2 GB</span>
        </div>
      </div>
      
      <div className="hidden sm:block">
        v1.0.0
      </div>
    </footer>
  );
}
