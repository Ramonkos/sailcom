import { ADD_BOAT, ADD_BOOKING_TO_BOAT, GET_ALL_BOAT_INFO } from '../constants';

const initialState = {
    boatlist: {},
    boatOverview: null,
};

export const boats = (state = initialState, action) => {

    switch (action.type) {
        case ADD_BOAT:
            const new_key = action.id;
            return {
                ...state,
                boatlist: {
                    ...state.boatlist,
                    [new_key]: action.payload,
                },
            };

        case GET_ALL_BOAT_INFO:
            return {
                ...state,
                boatOverview: action.payload,
            };

        case ADD_BOOKING_TO_BOAT:
            const boat_key = action.boat_id;
            const new_bookings_array = state.boatlist[boat_key].bookings;
            new_bookings_array.push(action.payload);
            return {
                ...state,
                boatlist: {
                    ...state.boatlist,
                    [boat_key]: {
                        ...state.boatlist[boat_key],
                        bookings: new_bookings_array,
                    },
                },
            };

        default:
            return state;
    }
};
