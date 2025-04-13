const DigitalSouvenirs = () => {
  const souvenirs = [
    {
      icon: 'https://via.placeholder.com/100',
      title: 'Тамань',
    },
    {
      icon: 'https://via.placeholder.com/100',
      title: 'Сочи',
    },
    {
      icon: 'https://via.placeholder.com/100',
      title: 'Геленджик',
    },
  ];

  return (
    <div className="mb-8">
      <h3 className="text-xl font-semibold text-gray-800 mb-4 text-center">Цифровые сувениры</h3>
      <div className="grid grid-cols-3 gap-10">
        {souvenirs.map((souvenir, index) => (
          <div key={index} className="flex flex-col items-center space-y-2">
            <img
              src="./nft.png"
              alt={souvenir.title}
              className="w-20 h-20 rounded-lg object-cover"
            />
            <p className="text-sm text-center font-medium text-black">{souvenir.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DigitalSouvenirs;