import { Search, Menu, Bell, HelpCircle, Maximize2 } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';

interface TopBarProps {
  onToggleSidebar: () => void;
  sidebarCollapsed: boolean;
}

export function TopBar({ onToggleSidebar, sidebarCollapsed }: TopBarProps) {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 gap-4 flex-shrink-0">
      {/* Left Section */}
      <div className="flex items-center gap-4 flex-1">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleSidebar}
          className="flex-shrink-0"
        >
          <Menu className="w-5 h-5" />
        </Button>

        {/* Search */}
        <div className="relative max-w-md w-full hidden sm:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            type="search"
            placeholder="Search..."
            className="pl-10 bg-gray-50"
          />
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" className="relative hidden sm:flex">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
        </Button>

        <Button variant="ghost" size="icon" className="hidden md:flex">
          <HelpCircle className="w-5 h-5" />
        </Button>

        <Button variant="ghost" size="icon" className="hidden md:flex">
          <Maximize2 className="w-5 h-5" />
        </Button>
      </div>
    </header>
  );
}
