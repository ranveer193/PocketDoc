export default function DiseaseResults({ data }) {
  return (
    <div className="space-y-2">
      {data.map((p, i) => (
        <div key={i}>
          <div className="flex justify-between text-sm font-semibold">
            <span>{p.disease}</span>
            <span>{(p.confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="h-2 w-full bg-slate-300 rounded">
            <div
              className="h-2 bg-green-500 rounded"
              style={{ width: `${p.confidence * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
