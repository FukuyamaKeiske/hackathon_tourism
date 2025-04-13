import { APIInterests, APIRoute } from './types'
import { API_URL, TOKEN } from './constants'

const register = async (email: string, password: string, interests: APIInterests) => {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            email: email,
            password: password,
            interests: {
                dest: interests.where,
                with: interests.withWho,
                food: interests.food
            }
         }),
    })
    return response.json()
}

const login = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            email: email,
            password: password
         }),
    })
    return response.json()
}

const getInterests = async () => {
    const response = await fetch(`${API_URL}/profile/interests`, {
        method: 'GET',
    })
    return response.json() as Promise<APIInterests>
}

const getRoute = async (lat: string, lng: string) => {
    const response = await fetch(`${API_URL}/recommendations/route?lat=${lat}&lng=${lng}`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${TOKEN}`,
            "Access-Control-Allow-Origin": '*'
        },
    })
    return response.json() as Promise<APIRoute[]>
}

export { register, login, getInterests, getRoute }