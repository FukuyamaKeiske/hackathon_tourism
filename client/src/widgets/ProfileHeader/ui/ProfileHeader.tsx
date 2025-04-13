const ProfileHeader = () => {
  return (
    <div className="flex items-center justify-center mt-5 flex-col">
      <div>
        <div className="w-32 h-32 rounded-full bg-black overflow-hidden">
        </div>
      </div>

      {/* Информация о пользователе */}
      <div className="flex flex-col">
        <h2 className="text-2xl font-bold text-gray-800 text-center">Ли Чжан</h2>
        <div className="mt-10 space-y-1 flex gap-5 text-center">
          <p className="flex items-center flex-col text-gray-600">
            <a className="text-sm">В путешествии</a>
            <div className="flex items-center gap-2">
                <img src="./clock.png" className="w-4 h-4"/>
                <span className="text-[#370A27]">1 день</span>
            </div>
          </p>
          <p className="flex items-center flex-col text-gray-600">
            <a className="text-sm">Пройдено</a>
            <div className="flex items-center gap-2">
                <img src="./clock.png" className="w-4 h-4"/>
                <span className="text-[#370A27]">0km</span>
            </div>
          </p>
          <p className="flex items-center flex-col text-gray-600">
            <a className="text-sm">Ранг туриста</a>
            <div className="flex items-center gap-2">
                <img src="./clock.png" className="w-4 h-4"/>
                <span className="text-[#370A27]">5 ранг</span>
            </div>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProfileHeader;