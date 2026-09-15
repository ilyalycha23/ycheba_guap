// Описывает переиспользуемую карточку одной возможности приложения.

// Типизируем входные свойства компонента.
type FeatureCardProps = Readonly<{
  title: string;
  description: string;
}>;

// Объявляем основной компонент этого файла.
export default function FeatureCard({
  title,
  description,
}: FeatureCardProps) {
  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <article className="feature-card">
      <h3>{title}</h3>
      <p>{description}</p>
    </article>
  );
}
