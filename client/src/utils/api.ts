import 'dotenv/config'
import { APIInterests } from './types'

const API_URL = process.env.API_URL

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
                "куда": interests.where,
                "с кем": interests.withWho,
                "еда": interests.food
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

const changeInterests = async (token: string, interests: APIInterests) => {
    const response = await fetch(`${API_URL}/profile/interests`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ 
            interests: {
                "куда": interests.where,
                "с кем": interests.withWho,
                "еда": interests.food
            }
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

export { register, login, changeInterests, getInterests }