import { Ingredient } from './IngredientList';
import { Beaker, Percent } from 'lucide-react';
import { Card } from './ui/card';

interface FormulaSummaryProps {
  ingredients: Ingredient[];
}

export function FormulaSummary({ ingredients }: FormulaSummaryProps) {
  // Calculate total quantity
  const totalQuantity = ingredients.reduce((sum, ing) => {
    const qty = parseFloat(ing.quantity) || 0;
    return sum + qty;
  }, 0);

  // Calculate percentages
  const ingredientsWithPercentages = ingredients.map(ing => {
    const qty = parseFloat(ing.quantity) || 0;
    const percentage = totalQuantity > 0 ? (qty / totalQuantity) * 100 : 0;
    return {
      ...ing,
      percentage: percentage.toFixed(2)
    };
  });

  // Filter out empty ingredients
  const validIngredients = ingredientsWithPercentages.filter(ing => 
    ing.name.trim() !== '' && parseFloat(ing.quantity) > 0
  );

  if (validIngredients.length === 0) {
    return null;
  }

  return (
    <Card className="bg-slate-900/75 backdrop-blur-sm border-3 border-emerald-500/40 p-4 pixel-corners relative overflow-hidden">
      {/* Corner decorations */}
      <div className="absolute top-1 left-1 w-2 h-2 bg-emerald-400 animate-pulse" />
      <div className="absolute top-1 right-1 w-2 h-2 bg-emerald-400 animate-pulse" style={{ animationDelay: '0.5s' }} />
      
      <div className="space-y-3">
        {/* Header */}
        <div className="flex items-center gap-3 pb-2 border-b-2 border-emerald-500/30">
          <div className="p-2 bg-emerald-500/30 border-2 border-emerald-400/60"
            style={{ imageRendering: 'pixelated' }}
          >
            <Beaker className="w-5 h-5 text-emerald-300" strokeWidth={2.5} />
          </div>
          <div>
            <h3 className="text-sm text-emerald-300 pixel-text">⚗ Formula Summary</h3>
            <p className="text-xs text-emerald-200/60 font-mono">
              Total: {totalQuantity.toFixed(2)} {validIngredients[0]?.unit || 'units'}
            </p>
          </div>
        </div>

        {/* Ingredients Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-2">
          {validIngredients.map((ing) => (
            <div
              key={ing.id}
              className="bg-slate-800/50 border-2 border-emerald-500/30 p-2.5 pixel-corners hover:border-emerald-400/50 transition-colors relative group"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-emerald-300 font-mono truncate">
                    {ing.name}
                  </p>
                  <p className="text-xs text-emerald-200/60 font-mono">
                    {parseFloat(ing.quantity).toFixed(2)} {ing.unit}
                  </p>
                </div>
                <div className="flex items-center gap-1 flex-shrink-0">
                  <Percent className="w-3 h-3 text-emerald-400" />
                  <span className="text-sm text-emerald-400 font-mono">
                    {ing.percentage}
                  </span>
                </div>
              </div>
              
              {/* Optimization indicator */}
              {ing.includeInOptimization && (
                <div className="absolute bottom-1 right-1 w-1.5 h-1.5 bg-yellow-400 rounded-full animate-pulse" 
                  title="Included in optimization" 
                />
              )}
            </div>
          ))}
        </div>

        {/* Total Bar */}
        <div className="bg-slate-800/50 border-2 border-emerald-500/30 p-2 pixel-corners">
          <div className="flex items-center justify-between">
            <span className="text-xs text-emerald-300 font-mono">Total Percentage:</span>
            <span className="text-sm text-emerald-400 font-mono">100.00%</span>
          </div>
        </div>
      </div>
    </Card>
  );
}
