import React, {useEffect, useState} from "react";
import SelectLake from "./selectLake";
import SelectCategory from "./selectCategory";
import PeriodPicker from "./periodPicker";
import {connect} from "react-redux";
import UserAddressForm from "../../UserAddress";
import UserDocumentsForm from "../../UserDocuments";
import UserTransactions from "../../UserTransactions";

function BoatListFilter(props) {
    const [formState, setFormState] = useState({})

    const onChangeHandler = (e) => {
        const key = e.currentTarget.name;
        setFormState({
            ...formState,
            [key]: e.currentTarget.value,
        });
    };

    const onChangeDateHandler = (date, key) => {
        console.log(formState)
        setFormState({
            ...formState,
            [key]: date,
        });
    };

    return (
            <div className='filter-container'>
                <h1>Boot finden</h1>
                <form className='filter-form col-2' onSubmit={ e => props.submitFilterHandler(e, formState) }>
                    <div className="input-container">
                        <SelectLake onChangeHandler={onChangeHandler}/>
                        <SelectCategory onChangeHandler={onChangeHandler} />
                        <PeriodPicker
                            onChangeDateHandler={onChangeDateHandler}
                            from={formState['from_date_time']}
                            until={formState['until_date_time']}
                        />
                        {
                            props.currentUser.authorized
                            ?
                                <div className='input-wrapper checkbox'>
                                    <input type="checkbox" id="instructed" name="instructed" value="true" />
                                    <label htmlFor="instructed"> Nur von mir eingesegelte Botte anzeigen</label>
                                </div>
                            : null
                        }
                    </div>
                    <button className='btn primary' type='submit' onClick={ e => props.submitFilterHandler(e, formState) }>Suchen</button>
                </form>
            </div>
    );
};


const mapStateToProps = (state) => {
    return {
        currentUser: state.currentUser    }
}
const connection = connect(mapStateToProps);
const ConnectedBoatListFilter = connection(BoatListFilter);

export default ConnectedBoatListFilter;