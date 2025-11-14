import { DashboardView } from './views/DashboardView';
import { DocumentsView } from './views/DocumentsView';
import { GenericView } from './views/GenericView';

interface MainContentProps {
  activeView: string;
}

export function MainContent({ activeView }: MainContentProps) {
  return (
    <main className="flex-1 overflow-auto bg-gray-50">
      <div className="p-6">
        {activeView === 'dashboard' && <DashboardView />}
        {activeView === 'documents' && <DocumentsView />}
        {activeView !== 'dashboard' && activeView !== 'documents' && (
          <GenericView viewName={activeView} />
        )}
      </div>
    </main>
  );
}
