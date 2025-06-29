import { useState } from 'react';
import { Star } from 'lucide-react';

export default function RatingStars({ onRate }) {
  const [val, setVal] = useState(0);
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map((i) => (
        <Star
          key={i}
          size={22}
          className={`cursor-pointer ${
            i <= val ? 'text-yellow-400' : 'text-slate-400'
          }`}
          onMouseEnter={() => setVal(i)}
          onClick={() => onRate(i)}
        />
      ))}
    </div>
  );
}
