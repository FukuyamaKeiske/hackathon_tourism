import { Suspense, lazy } from "react"
import { BrowserRouter, Route, Routes } from "react-router"

const LazyPopularPlaces = lazy(() => import('./pages/PopularPlaces'))

function App() {

  return (
    <>
      <BrowserRouter>
          <Suspense fallback={<div>Loading...</div>}>
            <Routes>
                <Route path="/" element={<LazyPopularPlaces />} />
            </Routes>
          </Suspense>
      </BrowserRouter>
    </>
  )
}

export default App
