const Achievements = () => {
  const achievements = [
    {
      icon: '',
      title: 'Знаток Кубани',
    },
    {
      icon: 'https://via.placeholder.com/100',
      title: 'Герой Экстрима',
    },
    {
      icon: 'https://via.placeholder.com/100',
      title: 'Историк Тамани',
    },
  ];

  return (
    <div className="mb-8">
      <div className="grid grid-cols-3 gap-4 mt-2">
        {achievements.map((achievement, index) => (
          <div key={index} className="flex flex-col items-center space-y-2">
            <img
              src="./achieve.png"
              alt={achievement.title}
              className="w-20 h-20 rounded-full object-cover"
            />
            <p className="text-xl font-semibold text-center text-gray-700">{achievement.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Achievements;