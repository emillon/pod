(import
    [app [db]]
    [sqlalchemy.orm.exc [NoResultFound]]
    [models [User]]
    [bcrypt]
)

(defn auth_user [login password]
    (let [[user
            (try 
                (->
                    (db.session.query User)
                    (.filter (= User.name login))
                    (.one))
                (catch [NoResultFound] None))
         ]]
        (if (none? user)
            user
            (let [[db_hash user.password]
                  [hashed (bcrypt.hashpw (password.encode "utf-8")
                                         (db_hash.encode "ascii")
                          )]
                 ]
                (if (!= db_hash hashed)
                    None
                    user
                )
            )
        )
    )
)
