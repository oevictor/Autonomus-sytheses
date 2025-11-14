import { Card } from '../ui/card';

interface GenericViewProps {
  viewName: string;
}

export function GenericView({ viewName }: GenericViewProps) {
  const formattedName = viewName.charAt(0).toUpperCase() + viewName.slice(1);
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-gray-900 mb-2">{formattedName}</h1>
        <p className="text-gray-600">This is the {formattedName.toLowerCase()} section of your application.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <Card key={i} className="p-6">
            <div className="h-32 bg-gray-100 rounded-lg mb-4" />
            <h3 className="text-gray-900 mb-2">Content Card {i}</h3>
            <p className="text-sm text-gray-600">
              Placeholder content for the {formattedName.toLowerCase()} view.
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
}
