import { Suspense, lazy } from "react"
import { BrowserRouter, Route, Routes } from "react-router"

const LazyPopularPlaces = lazy(() => import('./pages/PopularPlaces'))
const LazyProfile = lazy(() => import('./pages/Profile'))
const LazyMap = lazy(() => import('./pages/Map'))
const LazyQuests = lazy(() => import('./pages/Quests'))

function App() {

  return (
    <>
      <BrowserRouter>
          <Suspense fallback={<div>Loading...</div>}>
            <Routes>
                <Route path="/" element={<LazyMap />} />
                <Route path="/quests" element={<LazyQuests />} />
                <Route path="/popular-places" element={<LazyPopularPlaces />} />
                <Route path="/profile" element={<LazyProfile />} />
            </Routes>
          </Suspense>
      </BrowserRouter>
    </>
  )
}

export default App
