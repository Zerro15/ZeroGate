interface Props {
  values: number[];
}

export default function Sparkline({ values }: Props) {
  const max = Math.max(...values, 1);
  return (
    <div className="flex h-16 items-end gap-1">
      {values.map((v, idx) => (
        <div
          key={idx}
          className="flex-1 rounded-md bg-primary-500/70 dark:bg-primary-400/80"
          style={{ height: `${(v / max) * 100}%` }}
        />
      ))}
    </div>
  );
}
