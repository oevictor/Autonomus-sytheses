import { Trash2, Copy, Droplet, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Switch } from './ui/switch';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';
import { Card } from './ui/card';
import { Ingredient } from './IngredientList';

interface IngredientCardProps {
  ingredient: Ingredient;
  index: number;
  onUpdate: (id: string, updates: Partial<Ingredient>) => void;
  onRemove: (id: string) => void;
  onDuplicate: (id: string) => void;
  canRemove: boolean;
}

const metricUnits = ['g', 'kg', 'mg', 'mL', 'L'];
const imperialUnits = ['oz', 'lb', 'fl oz', 'gal', 'tsp', 'tbsp'];

export function IngredientCard({
  ingredient,
  index,
  onUpdate,
  onRemove,
  onDuplicate,
  canRemove,
}: IngredientCardProps) {
  const units = ingredient.measurementSystem === 'metric' ? metricUnits : imperialUnits;

  return (
    <Card className="bg-slate-900/75 backdrop-blur-sm border-3 border-cyan-500/40 p-4 hover:border-cyan-400/60 transition-all hover:shadow-[0_0_20px_rgba(34,211,238,0.15)] pixel-corners relative">
      {/* Animated corner indicator */}
      <div className="absolute top-1 right-1 w-2 h-2 bg-cyan-400 animate-pulse" />
      
      <div className="space-y-4">
        {/* Compact Header */}
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-cyan-500/30 border-2 border-cyan-400/60"
              style={{ imageRendering: 'pixelated' }}
            >
              <Droplet className="w-4 h-4 text-cyan-300" strokeWidth={2.5} />
            </div>
            <div>
              <h3 className="text-sm text-cyan-300 pixel-text">⬢ Ingredient #{index + 1}</h3>
            </div>
          </div>
          
          <div className="flex gap-1">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDuplicate(ingredient.id)}
              className="h-7 w-7 text-cyan-400 hover:text-cyan-300 hover:bg-cyan-500/20 border-2 border-transparent hover:border-cyan-500/40 pixel-button"
            >
              <Copy className="w-3 h-3" />
            </Button>
            {canRemove && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onRemove(ingredient.id)}
                className="h-7 w-7 text-red-400 hover:text-red-300 hover:bg-red-500/20 border-2 border-transparent hover:border-red-500/40 pixel-button"
              >
                <Trash2 className="w-3 h-3" />
              </Button>
            )}
          </div>
        </div>

        {/* Compact Basic Information */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="col-span-2 space-y-1.5">
            <Label htmlFor={`name-${ingredient.id}`} className="text-xs text-cyan-200 font-mono">
              ▸ Name
            </Label>
            <Input
              id={`name-${ingredient.id}`}
              value={ingredient.name}
              onChange={(e) => onUpdate(ingredient.id, { name: e.target.value })}
              placeholder="e.g., Sodium Chloride"
              className="h-8 text-sm bg-slate-800/60 border-2 border-cyan-500/40 text-cyan-100 placeholder:text-cyan-200/30 focus:border-cyan-400 pixel-input font-mono"
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor={`quantity-${ingredient.id}`} className="text-xs text-cyan-200 font-mono">
              ▸ Qty
            </Label>
            <Input
              id={`quantity-${ingredient.id}`}
              type="number"
              value={ingredient.quantity}
              onChange={(e) => onUpdate(ingredient.id, { quantity: e.target.value })}
              placeholder="0.00"
              className="h-8 text-sm bg-slate-800/60 border-2 border-cyan-500/40 text-cyan-100 placeholder:text-cyan-200/30 focus:border-cyan-400 pixel-input font-mono"
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor={`unit-${ingredient.id}`} className="text-xs text-cyan-200 font-mono">
              ▸ Unit
            </Label>
            <Select
              value={ingredient.unit}
              onValueChange={(value) => onUpdate(ingredient.id, { unit: value })}
            >
              <SelectTrigger 
                id={`unit-${ingredient.id}`}
                className="h-8 text-sm bg-slate-800/60 border-2 border-cyan-500/40 text-cyan-100 focus:border-cyan-400 pixel-input font-mono"
              >
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800/95 border-3 border-cyan-500/40 backdrop-blur-sm">
                {units.map((unit) => (
                  <SelectItem 
                    key={unit} 
                    value={unit} 
                    className="text-sm text-cyan-100 focus:bg-cyan-500/30 font-mono pixel-corners"
                  >
                    {unit}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Compact Measurement System */}
        <div className="flex gap-2">
          <Button
            type="button"
            size="sm"
            variant={ingredient.measurementSystem === 'metric' ? 'default' : 'outline'}
            onClick={() => {
              onUpdate(ingredient.id, { 
                measurementSystem: 'metric',
                unit: 'g' 
              });
            }}
            className={
              ingredient.measurementSystem === 'metric'
                ? 'h-7 text-xs bg-cyan-600 hover:bg-cyan-500 text-white border-2 border-cyan-400/60 pixel-button shadow-[0_0_10px_rgba(34,211,238,0.2)]'
                : 'h-7 text-xs border-2 border-cyan-500/40 text-cyan-300 hover:bg-cyan-500/20 pixel-button'
            }
          >
            Metric
          </Button>
          <Button
            type="button"
            size="sm"
            variant={ingredient.measurementSystem === 'imperial' ? 'default' : 'outline'}
            onClick={() => {
              onUpdate(ingredient.id, { 
                measurementSystem: 'imperial',
                unit: 'oz' 
              });
            }}
            className={
              ingredient.measurementSystem === 'imperial'
                ? 'h-7 text-xs bg-cyan-600 hover:bg-cyan-500 text-white border-2 border-cyan-400/60 pixel-button shadow-[0_0_10px_rgba(34,211,238,0.2)]'
                : 'h-7 text-xs border-2 border-cyan-500/40 text-cyan-300 hover:bg-cyan-500/20 pixel-button'
            }
          >
            Imperial
          </Button>
        </div>

        {/* Compact Variation Range */}
        <div className="border-t-2 border-cyan-500/20 pt-3 space-y-3">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-purple-400 animate-pulse" />
            <h4 className="text-sm text-purple-300 pixel-text">Variation & Optimization</h4>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <Label htmlFor={`var-min-${ingredient.id}`} className="text-xs text-cyan-200 font-mono">
                ▸ Min (%)
              </Label>
              <Input
                id={`var-min-${ingredient.id}`}
                type="number"
                value={ingredient.variationMin}
                onChange={(e) => onUpdate(ingredient.id, { variationMin: e.target.value })}
                placeholder="-10"
                className="h-8 text-sm bg-slate-800/60 border-2 border-purple-500/40 text-purple-100 placeholder:text-purple-200/30 focus:border-purple-400 pixel-input font-mono"
              />
            </div>

            <div className="space-y-1.5">
              <Label htmlFor={`var-max-${ingredient.id}`} className="text-xs text-cyan-200 font-mono">
                ▸ Max (%)
              </Label>
              <Input
                id={`var-max-${ingredient.id}`}
                type="number"
                value={ingredient.variationMax}
                onChange={(e) => onUpdate(ingredient.id, { variationMax: e.target.value })}
                placeholder="+10"
                className="h-8 text-sm bg-slate-800/60 border-2 border-purple-500/40 text-purple-100 placeholder:text-purple-200/30 focus:border-purple-400 pixel-input font-mono"
              />
            </div>
          </div>

          <div className="flex items-center justify-between bg-slate-800/50 border-2 border-purple-500/30 p-2.5 pixel-corners relative">
            <div className="absolute top-0.5 left-0.5 w-1.5 h-1.5 bg-purple-400 animate-blink-slow" />
            <div className="flex items-center gap-2">
              <Label htmlFor={`optimize-${ingredient.id}`} className="text-xs text-purple-200 cursor-pointer font-mono">
                ⚡ Include in Optimization
              </Label>
            </div>
            <Switch
              id={`optimize-${ingredient.id}`}
              checked={ingredient.includeInOptimization}
              onCheckedChange={(checked) => 
                onUpdate(ingredient.id, { includeInOptimization: checked })
              }
              className="data-[state=checked]:bg-purple-600 scale-75"
            />
          </div>
        </div>
      </div>
    </Card>
  );
}
