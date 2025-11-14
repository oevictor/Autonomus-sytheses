import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { Search, Plus, Filter, FileText, Download, Trash2, MoreVertical } from 'lucide-react';

const documents = [
  { id: 1, name: 'Project Proposal.pdf', size: '2.4 MB', modified: '2024-11-10', type: 'PDF' },
  { id: 2, name: 'Budget Report.xlsx', size: '856 KB', modified: '2024-11-09', type: 'Excel' },
  { id: 3, name: 'Meeting Notes.docx', size: '124 KB', modified: '2024-11-08', type: 'Word' },
  { id: 4, name: 'Design Mockups.fig', size: '5.2 MB', modified: '2024-11-07', type: 'Figma' },
  { id: 5, name: 'Presentation.pptx', size: '3.1 MB', modified: '2024-11-06', type: 'PowerPoint' },
  { id: 6, name: 'Database Schema.sql', size: '45 KB', modified: '2024-11-05', type: 'SQL' },
  { id: 7, name: 'Marketing Plan.pdf', size: '1.8 MB', modified: '2024-11-04', type: 'PDF' },
  { id: 8, name: 'User Research.docx', size: '678 KB', modified: '2024-11-03', type: 'Word' },
];

export function DocumentsView() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-gray-900 mb-2">Documents</h1>
          <p className="text-gray-600">Manage and organize your files</p>
        </div>
        <Button className="flex items-center gap-2 w-full sm:w-auto">
          <Plus className="w-4 h-4" />
          Upload Document
        </Button>
      </div>

      {/* Search and Filter */}
      <Card className="p-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              type="search"
              placeholder="Search documents..."
              className="pl-10"
            />
          </div>
          <Button variant="outline" className="flex items-center gap-2">
            <Filter className="w-4 h-4" />
            <span className="hidden sm:inline">Filter</span>
          </Button>
        </div>
      </Card>

      {/* Documents Table */}
      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs text-gray-600 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs text-gray-600 uppercase tracking-wider hidden md:table-cell">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs text-gray-600 uppercase tracking-wider hidden sm:table-cell">
                  Size
                </th>
                <th className="px-6 py-3 text-left text-xs text-gray-600 uppercase tracking-wider hidden lg:table-cell">
                  Modified
                </th>
                <th className="px-6 py-3 text-right text-xs text-gray-600 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {documents.map((doc) => (
                <tr key={doc.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-blue-50 rounded">
                        <FileText className="w-4 h-4 text-blue-600" />
                      </div>
                      <span className="text-sm text-gray-900">{doc.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 hidden md:table-cell">
                    {doc.type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 hidden sm:table-cell">
                    {doc.size}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 hidden lg:table-cell">
                    {doc.modified}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <div className="flex items-center justify-end gap-2">
                      <Button variant="ghost" size="icon" className="hidden sm:flex">
                        <Download className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="hidden sm:flex">
                        <Trash2 className="w-4 h-4 text-red-600" />
                      </Button>
                      <Button variant="ghost" size="icon" className="sm:hidden">
                        <MoreVertical className="w-4 h-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
