interface Props {
  title: string;
  value: string;
  description?: string;
  accent?: 'green' | 'blue' | 'amber' | 'red';
}

const accents: Record<NonNullable<Props['accent']>, string> = {
  green: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-100',
  blue: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-100',
  amber: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-100',
  red: 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-100',
};

export default function StatCard({ title, value, description, accent = 'blue' }: Props) {
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</div>
          <div className="text-2xl font-semibold text-slate-900 dark:text-white">{value}</div>
          {description && <div className="text-xs text-slate-500 dark:text-slate-400">{description}</div>}
        </div>
        <div className={`rounded-full px-3 py-1 text-xs font-semibold ${accents[accent]}`}>{title}</div>
      </div>
    </div>
  );
}
