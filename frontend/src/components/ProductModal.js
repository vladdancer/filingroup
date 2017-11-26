import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'
import {NavLink} from 'react-router-dom'
import Masonry from 'react-masonry-component'

import {ObjToImmArr, createMarkup} from '../helpers'
import {loadPriveleges} from 'actions'

import Loader from 'components/Loader'
import ProductPrivileges from 'components/ProductPrivileges'
import CourseInfo from 'components/CourseInfo'
import CouchInfo from 'components/CouchInfo'
import ConsultInfo from 'components/ConsultInfo'
import RegisterForm from 'components/RegisterForm'

class ProductModal extends Component {
  componentDidMount = () => {
    const {loading, loaded, loadPriveleges} = this.props
    if(!loading && !loaded) loadPriveleges()
  }

  render(){
    const {priveleges, products, match, loading} = this.props
    const currentProduct = products.get(match.params.slug)
    const masonryOptions = {}
    const {
      id,
      title,
      slug,
      course_type,
      course_picture,
      discount,
      places,
      free_places,
      price,
      teachers,
      description
    } = currentProduct
    if(loading) return <Loader />
    console.log(title)
    return (
      <main className="main">
        <section className="section product__modal container">
          <ul className="breadcrumb__list">
            <li className="breadcrumb__item">
              <NavLink exact activeClassName='active' to='/'>Главная</NavLink>
            </li>
            <li className="breadcrumb__item">
              <NavLink exact activeClassName='active' to='/products'>Продукты</NavLink>
            </li>
            <li className="breadcrumb__item">
              <NavLink exact activeClassName='active' to={`/products/${slug}`}>{title}</NavLink>
            </li>
          </ul>
          <h1 className="section__title">{title}</h1>
          <div className="product__modal-main">
            <div className="product__modal-left">
              <img
                className="product__modal-pic"
                src={course_picture}
                alt="product"/>
              <ul className="product__modal-info">
                {this.getProductInfo(currentProduct)}
              </ul>
            </div>
            <div className="product__modal-right">
              <div dangerouslySetInnerHTML={createMarkup(description)}/>
            </div>
          </div>
          <Masonry
            className={'product__privileges-list'}
            elementType={'ul'}
            options={masonryOptions}
            disableImagesLoaded={false}
            updateOnEachImageLoad={false}
          >
            {priveleges.map(privelege => {
              return privelege.courses.map(course => {
                if(course.id === id) return <ProductPrivileges key={privelege.id} privelege = {privelege} />
              })
            })}
          </Masonry>
        </section>
        <RegisterForm courseId={id} />
      </main>
    )
  }
  getProductInfo = (currentProduct) => {
    const {course_type} = currentProduct
    switch(course_type.title){
      case "Коучинг":
        return <CouchInfo currentProduct={currentProduct}/>
      case "Консультация":
        return <ConsultInfo currentProduct={currentProduct}/>
      default:
        return <CourseInfo currentProduct={currentProduct}/>
    }
  }
}

export default connect(state => {
  return {
    products: state.products.entities,
    priveleges: ObjToImmArr(state.priveleges.entities),
    loading: state.priveleges.loading,
    loaded: state.priveleges.loaded
  }
}, {loadPriveleges})(ProductModal)