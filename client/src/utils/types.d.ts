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