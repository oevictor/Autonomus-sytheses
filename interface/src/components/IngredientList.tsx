import { useState } from 'react';
import { Plus, Save, FileDown } from 'lucide-react';
import { Button } from './ui/button';
import { IngredientCard } from './IngredientCard';
import { FormulaSummary } from './FormulaSummary';

export interface Ingredient {
  id: string;
  name: string;
  quantity: string;
  unit: string;
  measurementSystem: 'metric' | 'imperial';
  variationMin: string;
  variationMax: string;
  includeInOptimization: boolean;
}

export function IngredientList() {
  const [ingredients, setIngredients] = useState<Ingredient[]>([
    {
      id: '1',
      name: '',
      quantity: '',
      unit: 'g',
      measurementSystem: 'metric',
      variationMin: '',
      variationMax: '',
      includeInOptimization: true,
    }
  ]);

  const addIngredient = () => {
    const newIngredient: Ingredient = {
      id: Date.now().toString(),
      name: '',
      quantity: '',
      unit: 'g',
      measurementSystem: 'metric',
      variationMin: '',
      variationMax: '',
      includeInOptimization: true,
    };
    setIngredients([...ingredients, newIngredient]);
  };

  const updateIngredient = (id: string, updates: Partial<Ingredient>) => {
    setIngredients(ingredients.map(ing => 
      ing.id === id ? { ...ing, ...updates } : ing
    ));
  };

  const removeIngredient = (id: string) => {
    if (ingredients.length > 1) {
      setIngredients(ingredients.filter(ing => ing.id !== id));
    }
  };

  const duplicateIngredient = (id: string) => {
    const ingredient = ingredients.find(ing => ing.id === id);
    if (ingredient) {
      const newIngredient = {
        ...ingredient,
        id: Date.now().toString(),
        name: ingredient.name + ' (copy)',
      };
      setIngredients([...ingredients, newIngredient]);
    }
  };

  return (
    <div className="space-y-4">
      {/* Formula Summary Banner */}
      <FormulaSummary ingredients={ingredients} />

      {/* Action Bar */}
      <div className="flex flex-col sm:flex-row gap-3 justify-between items-start sm:items-center bg-slate-900/70 backdrop-blur-sm border-3 border-cyan-500/40 p-4 pixel-corners relative overflow-hidden">
        {/* Corner decorations */}
        <div className="absolute top-0 left-0 w-3 h-3 border-t-3 border-l-3 border-cyan-400 animate-pulse" />
        <div className="absolute top-0 right-0 w-3 h-3 border-t-3 border-r-3 border-cyan-400 animate-pulse" style={{ animationDelay: '0.5s' }} />
        <div className="absolute bottom-0 left-0 w-3 h-3 border-b-3 border-l-3 border-cyan-400 animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute bottom-0 right-0 w-3 h-3 border-b-3 border-r-3 border-cyan-400 animate-pulse" style={{ animationDelay: '1.5s' }} />
        
        <div className="relative z-10">
          <h2 className="text-sm text-cyan-300 pixel-text">⚗ Ingredients</h2>
          <p className="text-xs text-cyan-200/70 font-mono">
            [{ingredients.length}] loaded
          </p>
        </div>
        
        <div className="flex gap-2 w-full sm:w-auto relative z-10">
          <Button
            onClick={addIngredient}
            className="flex-1 sm:flex-none h-8 text-xs bg-cyan-600 hover:bg-cyan-500 text-white border-3 border-cyan-400/60 pixel-button shadow-[0_0_15px_rgba(34,211,238,0.2)] transition-all hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]"
          >
            <Plus className="w-3 h-3 mr-1" />
            Add Ingredient
          </Button>
          
          <Button
            variant="outline"
            className="h-8 text-xs border-3 border-cyan-500/60 text-cyan-300 hover:bg-cyan-500/20 pixel-button hidden sm:flex shadow-[0_0_10px_rgba(34,211,238,0.15)]"
          >
            <Save className="w-3 h-3 mr-1" />
            Save
          </Button>
          
          <Button
            variant="outline"
            className="h-8 text-xs border-3 border-emerald-500/60 text-emerald-300 hover:bg-emerald-500/20 pixel-button hidden sm:flex shadow-[0_0_10px_rgba(16,185,129,0.15)]"
          >
            <FileDown className="w-3 h-3 mr-1" />
            Export
          </Button>
        </div>
      </div>

      {/* Ingredient Cards */}
      <div className="space-y-3">
        {ingredients.map((ingredient, index) => (
          <IngredientCard
            key={ingredient.id}
            ingredient={ingredient}
            index={index}
            onUpdate={updateIngredient}
            onRemove={removeIngredient}
            onDuplicate={duplicateIngredient}
            canRemove={ingredients.length > 1}
          />
        ))}
      </div>

      {/* Mobile Action Buttons */}
      <div className="flex gap-2 sm:hidden">
        <Button
          variant="outline"
          className="flex-1 h-8 text-xs border-3 border-cyan-500/60 text-cyan-300 hover:bg-cyan-500/20 pixel-button"
        >
          <Save className="w-3 h-3 mr-1" />
          Save
        </Button>
        
        <Button
          variant="outline"
          className="flex-1 h-8 text-xs border-3 border-emerald-500/60 text-emerald-300 hover:bg-emerald-500/20 pixel-button"
        >
          <FileDown className="w-3 h-3 mr-1" />
          Export
        </Button>
      </div>
    </div>
  );
}