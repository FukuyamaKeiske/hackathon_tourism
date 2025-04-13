export interface APIInterests {
    where: string[];
    withWho: string[];
    food: string[];
}

export interface APIRoute {
    id: string;
    name: string;
    description: string;
    coordinates: {
        lat: number;
        lng: number;
    };
    type: string;
    cuisine: string;
    halal: string;
    gallery: string[];
    partner?: boolean;
    work_time?: string;
}

export interface APIQuest {
    id: string;
    location: string;
    title: string;
    description: string;
    coordinates: {
        lat: number;
        lng: number;
    };
    link?: string;
    reward_points: number;
    total_steps: number;
    completed: boolean;
    progress: number;
    completed_steps: number;
}